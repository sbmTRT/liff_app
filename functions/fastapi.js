const { exec } = require('child_process');

exports.handler = async function(event, context) {
  try {
    const command = `python -m uvicorn app:app --host 0.0.0.0 --port ${process.env.PORT || 8888} --reload`;
    
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        return;
      }
      if (stderr) {
        console.error(`Stderr: ${stderr}`);
        return;
      }
      console.log(`Server started: ${stdout}`);
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ status: "success" }),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ status: "error", error: error.message }),
    };
  }
};
