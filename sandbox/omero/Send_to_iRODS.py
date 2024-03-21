#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
  Copyright (C) 2024 German BioImaging. All rights reserved.


  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

------------------------------------------------------------------------------

This script uses omero-cli-transfer to package data in
this OMERO instance for archiving to iRODS.

"""

import omero.scripts as scripts
from omero.gateway import BlitzGateway
import omero.util.script_utils as script_utils
import omero
from omero.cli import CLI
from omero.rtypes import rstring, rlong, robject
import os

from datetime import datetime
from typing import List


# keep track of log strings.
log_strings = []


def log(text):
    print(text)


def call_omero_transfer(command: List[str]):

    environment = os.environ.copy()
    del environment["OMERO_HOME"]  # Prevents warning


    pre_arguments = [
            "omero",
            # TODO: FIXME since this should make use of the Router
            "-q",
            "transfer",
            "pack",
    ]

    post_arguments = [
            "transfer.tar",
    ]

    process = subprocess.check_call(
            pre_arguments + command + post_arguments,
            env=environment,
    )


def invoke_omero_transfer(conn, command: List[str]):

    # Temporarily use the active session in a new client
    # This is needed since `omero transfer` is requesting
    # stdin even though ICE_CONFIG is set.
    client = conn.c.createClient(secure=False)
    fixme = client.getSessionId()

    pre_arguments = [
            # TODO: remove along with the above
            "-q", "-s", "localhost", "-k", fixme,
            "transfer",
            "pack",
    ]

    post_arguments = [
            "transfer.tar",
    ]

    cli = CLI()
    cli.loadplugins()
    cli.set_client(conn.c.createClient(secure=False))
    del cli.controls["sessions"]
    transfer = cli.controls["transfer"]
    assert transfer.ctx.conn()
    cli.onecmd(pre_arguments + command + post_arguments)


def transfer_to_irods_as_admin(source:str, output_path:str):
    import os
    import ssl
    from irods.session import iRODSSession
    try:
        env_file = os.environ['IRODS_ENVIRONMENT_FILE']
    except KeyError:
        env_file = os.path.expanduser('~/.irods/irods_environment.json')

    ssl_settings = {}  # FIXME

    with iRODSSession(
            user="SCRIPT_RUNNING_USER",
            irods_env_file=env_file,
            **ssl_settings) as session:

        # Tranfer the package
        session.data_objects.put(source, output_path)


def transfer_to_irods(source:str, output_path:str):
    import irods
    import os
    import ssl
    from irods.session import iRODSSession


    with iRODSSession(host='irods-catalog-provider', port=1247, user='rods', password='rods', zone='tempZone') as session:

        try:
            # Check for existence
            log('Checking existence of [{}] in iRODS...'.format(output_path))
            session.data_objects.get(output_path)
            log('- Found in iRODS - Skipping.'.format(output_path))
        except irods.exception.DataObjectDoesNotExist as e:
            # Transfer the package
            log('- Transferring...'.format(output_path))
            session.data_objects.put(source, output_path)
            log('- Complete.')

def send_to_irods(conn, script_params):
    data_type = script_params["Data_Type"]
    output_path = script_params["Path"]

    # Get the images or datasets
    message = ""
    objects, log_message = script_utils.get_objects(conn, script_params)
    message += log_message
    if not objects:
        return None, message

    # TODO: replace
    if data_type == "Dataset":
        images = []
        for ds in objects:
            images.extend(list(ds.listChildren()))
        if not images:
            message += "No image found in dataset(s)"
            return None, message
    else:
        images = objects

    log("Processing %s images" % len(images))

    # do the saving to disk
    for img in images:
        log("Processing image: ID %s: %s" % (img.id, img.getName()))
        invoke_omero_transfer(conn, [f"Image:{img.id}"])
        transfer_to_irods("transfer.tar", output_path)

    message = "transferred"
    return message


def run_script():
    """
    The main entry point of the script, as called by the client via the
    scripting service, passing the required parameters.
    """

    data_types = [rstring("Dataset"), rstring("Image")]

    client = scripts.client(
        "Send_to_iRODS.py",
        """Archive multiple images to iRODS in a zip file. \
See https://www.openmicroscopy.org/export.html#iRODS for more information""",
        scripts.String(
            "Data_Type",
            optional=False,
            grouping="1",
            description="The data you want to work with.",
            values=data_types,
            default="Image",
        ),
        scripts.List(
            "IDs",
            optional=False,
            grouping="2",
            description="List of Dataset IDs or Image IDs",
        ).ofType(rlong(0)),
        scripts.String(
            "Path",
            optional=False,
            grouping="3",
            description="iRODS Logical Path to which your archive should be uploaded",
        ),
        version="0.1.0",
        authors=["Josh Moore", "OME Team"],
        institutions=["German BioImaging"],
        contact="ome-users@lists.openmicroscopy.org.uk",
    )

    try:
        start_time = datetime.now()
        script_params = {}

        conn = BlitzGateway(client_obj=client)

        script_params = client.getInputs(unwrap=True)
        for key, value in script_params.items():
            log("%s:%s" % (key, value))

        # call the main script - returns a status message
        message = send_to_irods(conn, script_params)

        stop_time = datetime.now()
        log("Duration: %s" % str(stop_time - start_time))

        # return this message to the client.
        client.setOutput("Message", rstring(message))

    finally:
        client.closeSession()


if __name__ == "__main__":
    run_script()
