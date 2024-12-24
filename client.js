import dgram from "dgram";
import { get } from "http";
import readline from "readline";

const client = dgram.createSocket('udp4');

const post = 8080;
const host = "localhost";

const requestData = {
    id: 0,
    method: "",
    params: [],
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
        console.log(isNumericString(params[0]));
        return params.length == 1 && isNumericString(params[0]);
    } else if (method == "nroot") {
        return (
            params.length === 2 && params.every((param) => isNumericString(param))
        );
    } else if (method == "reverse") {
        return params.length === 1;
    } else if (method == "validAnagram") {
        return params.length === 2;
    } else if (method == "sort") {
        return params.length >= 1;
    } else {
        return false;
    }
}

async function getId() {
    while (true) {
        const id = await question("ID: ");

        requestData.id = Number(id);
        if (!isNaN(requestData.id)) {
            break;
        } else {
            console.log("数値を入力してください");
        }
    }
}

async function getMethod() {
    while (true) {
        const method = await question("メソッド: ");

        requestData.method = method;
        if (methodList.includes(method)) {
            break;
        } else {
            console.log("有効なメソッドを入力してください");
        }
    }
}

async function getParams() {
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

function connectToServer() {
    client.send(JSON.stringify(requestData), 0, JSON.stringify(requestData).length, post, host, (err, bytes) => {
        console.log(`リクエスト: ${JSON.stringify(requestData)}`);
    })
}

function setupClientHandlers() {
    client.on("message", (msg, rinfo) => {
        console.log(`レスポンス: ${msg.toString("utf-8")}`)
        client.close()
    })

    client.on("error", (err) => {
        console.log(`client error \n ${err.stack}`)
        console.close()
    })

    client.on("close", () => {
        console.log("接続が閉じられました");
    });
}

async function main() {
    await getId();
    await getMethod();
    await getParams();
    connectToServer();    
    setupClientHandlers()
}

main();
