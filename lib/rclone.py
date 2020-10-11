"""
A Python wrapper for rclone.
"""
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
import subprocess
import tempfile
from os import path


class RCloneWrapper:
    """
    Wrapper class for rclone.
    """

    def __init__(self, cfg):
        if path.isfile(cfg):
            self.cfgFile = cfg
        else:
            self.tempFolder = tempfile.TemporaryDirectory()
            self.cfgFile = tempfile.NamedTemporaryFile(mode='w+', dir=self.tempFolder.name, delete=False).name
            with open(self.cfgFile,"w") as cfgFile:
                cfgFile.write(cfg)
        self.log = logging.getLogger("RClone")

    def _execute(self, command_with_args):
        """
        Execute the given `command_with_args` using Popen

        Args:
            - command_with_args (list) : An array with the command to execute,
                                         and its arguments. Each argument is given
                                         as a new element in the list.
        """
        self.log.debug("Invoking : %s", " ".join(command_with_args))
        try:
            with subprocess.Popen(
                    command_with_args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE) as proc:
                (out, err) = proc.communicate()

                #out = proc.stdout.read()
                #err = proc.stderr.read()

                self.log.debug(out)
                if err:
                    self.log.warning(err.decode("utf-8").replace("\\n", "\n"))

                return (proc.returncode, out, err)
        except FileNotFoundError as not_found_e:
            self.log.error("Executable not found. %s", not_found_e)
            return {
                "code": -20,
                "error": not_found_e
            }
        except Exception as generic_e:
            self.log.exception("Error running command. Reason: %s", generic_e)
            return {
                "code": -30,
                "error": generic_e
            }

    def run_cmd(self, command, extra_args=[]):
        """
        Execute rclone command

        Args:
            - command (string): the rclone command to execute.
            - extra_args (list): extra arguments to be passed to the rclone command
        """
        command_with_args = ["rclone", command, "--config", self.cfgFile]
        command_with_args += extra_args
        command_result = self._execute(command_with_args)
        return command_result

    def copy(self, source, dest, flags=[]):
        """
        Executes: rclone copy source:path dest:path [flags]

        Args:
        - source (string): A string "source:path"
        - dest (string): A string "dest:path"
        - flags (list): Extra flags as per `rclone copy --help` flags.
        """
        code, out, error = self.run_cmd(command="copy", extra_args=[source] + [dest] + flags)
        if code==0:
            return out.decode().splitlines()
        else:
            raise Exception

    def cat(self, source, flags=[]):
        """
        Executes: rclone cat source:path dest:path [flags]

        Args:
        - source (string): A string "source:path"
        - flags (list): Extra flags as per `rclone cat --help` flags.
        """
        code, out, error = self.run_cmd(command="cat", extra_args=[source] + flags)
        if code==0:
            return out.decode().splitlines()
        else:
            raise Exception

    def sync(self, source, dest, flags=[]):
        """
        Executes: rclone sync source:path dest:path [flags]

        Args:
        - source (string): A string "source:path"
        - dest (string): A string "dest:path"
        - flags (list): Extra flags as per `rclone sync --help` flags.
        """
        code, out, error = self.run_cmd(command="sync", extra_args=[source] + [dest] + flags)
        if code==0:
            return out.decode().splitlines()
        else:
            raise Exception

    def listremotes(self, flags=[]):
        """
        Executes: rclone listremotes [flags]

        Args:
        - flags (list): Extra flags as per `rclone listremotes --help` flags.
        """
        code, out, error = self.run_cmd(command="listremotes", extra_args=flags)
        if code==0:
            return out.decode().splitlines()
        else:
            raise Exception

    def lsf(self, dest=None, flags=[]):
        """
        Executes: rclone lsf remote:path [flags]

        Args:
        - dest (string): A string "remote:path" representing the location to list.
        """
        if dest is None:
            dest=self.destination
        code, out, error = self.run_cmd(command="lsf", extra_args=[dest] + flags)
        if code==0:
            return out.decode().splitlines()
        else:
            raise Exception

    def lsd(self, dest=None, flags=[]):
        """
        Executes: rclone lsd remote:path [flags]

        Args:
        - dest (string): A string "remote:path" representing the location to list.
        """
        if dest is None:
            dest=self.destination
        code, out, error = self.run_cmd(command="lsd", extra_args=[dest] + flags)
        if code==0:
            return out.decode().splitlines()
        else:
            raise Exception

    def lsjson(self, dest=None, flags=[]):
        """
        Executes: rclone lsjson remote:path [flags]

        Args:
        - dest (string): A string "remote:path" representing the location to list.
        """
        if dest is None:
            dest=self.destination
        code, out, error = self.run_cmd(command="lsjson", extra_args=[dest] + flags)
        if code==0:
            return out.decode()
        else:
            raise Exception

    def delete(self, dest=None, flags=[]):
        """
        Executes: rclone delete remote:path

        Args:
        - dest (string): A string "remote:path" representing the location to delete.
        """
        if dest is None:
            dest=self.destination
        code, out, error = self.run_cmd(command="delete", extra_args=[dest] + flags)
        if code==0:
            return out.decode()
        else:
            raise Exception

    @property
    def destination(self):
        if not hasattr(self, "__destination__"):
            remotes = self.listremotes()
            if len(remotes)==1:
                self.__destination__ = remotes[0]
            else:
                print("Multiple Destinations in config File")
                for index, destination in enumerate(remotes):
                    print (f"{index}: {destination}")
                index = int(input("Select default detination (0,1,2...) > "))
                self.__destination__ = remotes[index]
        return self.__destination__
    @destination.setter
    def destination(self, value):
        self.__destination__ = value
    
    def cd(self, string):   
        newDestination=self.destination
        for folder in string.split("/"):
            if newDestination[-1]==":":
                newDestination=newDestination+folder
            else:
                newDestination=path.join(newDestination,folder)
        try:
            self.lsd(newDestination)
            self.destination=newDestination
        except:
            print("not a valid directory")
        
    def size(self, dest=None, flags=[]):
        """
        Executes: rclone size remote:path

        Args:
        - dest (string): A string "remote:path" representing the location to get size from.
        """
        if dest is None:
            dest=self.destination
        code, out, error = self.run_cmd(command="size", extra_args=[dest] + flags)
        if code==0:
            return out.decode()
        else:
            raise Exception
        
    def tree(self, dest=None, flags=[]):
        """
        Executes: rclone tree remote:path

        Args:
        - dest (string): A string "remote:path" representing the location to get size from.
        """
        if dest is None:
            dest=self.destination
        code, out, error = self.run_cmd(command="size", extra_args=[dest] + flags)
        if code==0:
            return out.decode()
        else:
            raise Exception

def with_config(cfg):
    """
    Configure a new RClone instance.
    """
    inst = RClone(cfg=cfg)
    return inst

