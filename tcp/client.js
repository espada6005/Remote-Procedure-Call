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
    console.log("str", str);
    const num = Number(str);
    return !isNaN(num) && str === num.toString();
}

function validateParams(method, params) {
    console.log("method", method);

    console.log("params", params);
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

async function main() {

    while (true) {
        const id = await question("ID: ");

        requestData.id = Number(id);
        if (!isNaN(requestData.id)) {
            break;
        } else {
            console.log("数値を入力してください");
        }
    }
    while (true) {
        const method = await question("メソッド:");

        requestData.method = method;
        if (methodList.includes(method)) {
            break;
        } else {
            console.log("有効なメソッドを入力してください");
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

    client.connect(server_address, () => {
        console.log({ requestData });
        client.write(JSON.stringify(requestData));
    });

    client.on("data", (data) => {
        console.log(`レスポンス: ${data}`);
        client.destroy();
    });

    client.on("close", () => {
        console.log("接続が閉じられました");
    });

    client.on("error", (err) => {
        console.error(`error: ${err.message}`);
        process.exit(1);
    });
}

main();
