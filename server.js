const express = require("express");
const app = express();
const jwt = require('jsonwebtoken');
const axios = require('axios');
const multer = require("multer");
const admin = require('firebase-admin');
const { Firestore } = require("@google-cloud/firestore");
const { Storage } = require("@google-cloud/storage");
const { spawn } = require('child_process');

const serviceAccount = require('./serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  storageBucket: "gs://protelll.appspot.com"
});

const db = new Firestore({
  projectId: serviceAccount.project_id,
  credentials: {
    client_email: serviceAccount.client_email,
    private_key: serviceAccount.private_key,
  },
});

const storage = new Storage({
  projectId: serviceAccount.project_id,
  credentials: {
    client_email: serviceAccount.client_email,
    private_key: serviceAccount.private_key,
  },
});

app.use(express.json()); // Parse JSON bodies
app.use(express.urlencoded({ extended: true }));

const multerStorage = multer.memoryStorage();
const upload = multer({ storage: multerStorage });

app.post('/upload', upload.single('image'), async (req, res) => {
  const file = req.file;

  if (!file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  try {
    const bucket = admin.storage().bucket();
    const currentDate = new Date().toISOString().replace(/[-:.]/g, '');
    const uniqueFilename = currentDate + '-' + req.file.originalname;
    const fileUpload = bucket.file(uniqueFilename);
    const filePath = `${uniqueFilename}`;


    await fileUpload.save(file.buffer, {
      contentType: file.mimetype,
    });

    const signedUrl = `https://storage.googleapis.com/protelll.appspot.com/${filePath}`;

    const photoData = {
      url: signedUrl,
    };
    const docRef = await db.collection("file").add(photoData);

    const pythonProcess = spawn("C:\\Users\\Nathan\\AppData\\Local\\Programs\\Python\\Python311\\python.exe", [__dirname + "/app.py", signedUrl]);

    let prediction = "";
    let errorOutput = "";

    pythonProcess.stdout.on("data", (data) => {
      prediction += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      errorOutput += data.toString();
    });

    pythonProcess.on("close", async (code) => {
      console.log(`Child process exited with code ${code}`);

      if (code === 0) {
        prediction = prediction.replace(/\r?\n|\r/g, "");
        res.send({ prediction, imageUrl: signedUrl });
      } else {
        res.status(500).json({ error: "Internal server error", errorOutput });
      }
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to upload image' });
  }
});

app.listen(5000, () => {
  console.log(`Server running on port 5000`);
});
