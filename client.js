import net from "net";
import readline from "readline";

const client = new net.Socket();

const server_address = "./socket_file";

const requestData = {
    method: "",
    params: [],
    id: 0,
};

const methodList = ["floor", "nroot", "reverse", "validAnagram", "sort"];

