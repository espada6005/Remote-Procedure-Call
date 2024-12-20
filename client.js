import net from "net";
import { config } from "process";
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

function validateParams(method, params) {
    if (!Array.isArray(params)) {
        return false;
    }

    if (method == "floor") {
        return params.length === 1 && isNumericString(params[0]);
    } else if (method == "nroot") {
        return (
            params.length === 2 && params.every((params) => isNumericString(params))
        );
    } else if (method == "reverse") {
        return params.length === 1
    } else if (method == "validAnagram") {
        return params.length === 2;
    } else if (method == "sort") {
        return params.length >= 1;
    } else {
        return false;
    }
}

async function main() {
    while (true) {
        const id = await question("ID: ");

        requestData.id = Number(id);
        if (!isNaN(requestData.id)) {
            break;
        } else {
            console.log("数字を入力してください");
        }
    }

    while (true) {
        const method = await question("メソッド名を入力してください")

        requestData.method = method;
        if (methodList.includes(method)) {
            break;
        } else {
            console.log("有効なメソッド名を入力してください");
        }
    }

    while (true) {
        const paramsStr = await question("引数: ");

        const params = paramsStr.split(" ");

        if (validateParams(requestData.method, params)) {
            requestData.params = params;
            break;
        } else {
            console.log("有効な引数を入力してください");
        }
    }
}