require('dotenv').config();

const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

app.post('/runscript', (req, res) => {
    const { objective } = req.body;
    const pythonExecutable = process.env.PYTHON_EXECUTABLE;
    const absolutePathToScript = process.env.SCRIPT_PATH;

    const script = spawn(pythonExecutable, [absolutePathToScript, objective]);

    let outputData = '';
    let logData = '';

    script.stdout.on('data', (data) => {
        outputData += data.toString();
    });

    script.stderr.on('data', (data) => {
        // Accumulate log information and other error messages
        logData += data.toString();
    });

    script.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
        // Now send both the logs and output data together or separately as needed
        if (logData) {
            outputData = logData + '\n' + outputData; // Prepend log data to output
        }
        res.send(outputData);
    });
});

const PORT = 5001;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});