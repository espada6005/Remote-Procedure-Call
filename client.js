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

function question(query) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    return new Promise((resolve) => {
        rl.question(query, (answer) => {
            rl.close();
            resolve(answer);
        });
    });
}

function isNumericString(str) {
    const num = Number(str);
    return !isNaN(num) && str === num.toString();
}
