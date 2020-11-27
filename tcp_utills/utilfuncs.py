import argparse

port_number = 12345
buffer_size = 1024
default_buffer = buffer_size
server_name = "127.0.0.1"
break_char = "Ψ".encode("utf-8")

# in bytes
size_of_files = {
    "war_and_peace.txt": 3359584,
    "udolpho.txt": 1750348,
    "woman_in_white.txt": 1405831,
    "moby_dick.txt": 1276201,
    "don_quixote.txt": 2390853
}

def parse_args(protocol:str):
    parser = argparse.ArgumentParser(description="%s Server Script" % protocol)
    parser.add_argument(
        "-np", "--nonpers",
        help="uses connection non-persistently[persistent by default]",
        action="store_true"
    )

    args = parser.parse_args()
    return parser, args