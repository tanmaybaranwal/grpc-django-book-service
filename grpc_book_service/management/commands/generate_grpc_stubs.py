import pkg_resources
from django.core.management import BaseCommand
from grpc_tools import protoc


class Command(BaseCommand):
    help = "Generates server and client stubs using grpc_tools"

    def add_arguments(self, parser):
        parser.add_argument(
            "inclusion_root", nargs=1,
            help="Folder path where the target protos reside"
        )
        parser.add_argument(
            "proto_files", nargs=1,
            help="Comma separated values of proto files"
        )
        parser.add_argument(
            "--dest", dest="destination_path",
            help="Destination path of the generated stub outputs"
        )

    def handle(self, *args, **options):
        proto_files = options.get("proto_files")[0].split(",")
        inclusion_root = options["inclusion_root"][0]
        if options.get("destination_path"):
            destination_path = options["destination_path"]
        else:
            destination_path = "./"
        well_known_protos_include = pkg_resources.resource_filename(
            'grpc_tools', '_proto')
        for proto_file in proto_files:
            command = [
                "grpc_tools.protoc",
                "--proto_path={}".format(inclusion_root),
                "--proto_path={}".format(well_known_protos_include),
                "--python_out={}".format(destination_path),
                "--grpc_python_out={}".format(destination_path),
            ] + [proto_file]
            if protoc.main(command) != 0:
                self.stderr.write("Failed to generate {}".format(proto_file))
