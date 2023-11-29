const { exec } = require('child_process');

exports.handler = async function(event, context) {
  try {
    const command = `python -m uvicorn app:app --host 0.0.0.0 --port ${process.env.PORT || 8888} --reload`;

    exec(command, (error, stdout, stderr) => {
      if (error) {
        return {
          body: JSON.stringify({ message: error }),
        };
      }
      if (stderr) {
        return {
          body: JSON.stringify({ message: error }),
        };
      }
      return {
        body: JSON.stringify({ message: error }),
      };
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'SUCCESS Functions!' }),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ message: 'Error Functions!' }),
    };
  }
};
