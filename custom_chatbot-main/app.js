const express = require('express'); 								// https://www.npmjs.com/package/express
const session = require('express-session');							// https://www.npmjs.com/package/express-session
const passport = require('passport');
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');


const WebAppStrategy = require('ibmcloud-appid').WebAppStrategy;	// https://www.npmjs.com/package/ibmcloud-appid

const app = express();

// Configure multer to handle file uploads
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Warning The default server-side session storage implementation, MemoryStore, 
// is purposely not designed for a production environment. It will 
// leak memory under most conditions, it does not scale past a single process, 
// and is meant for debugging and developing.
// For a list of stores, see compatible session stores below
// https://www.npmjs.com/package/express-session#compatible-session-stores
app.use(session({
	secret: "123456",
	resave: true,
	saveUninitialized: true
}));
app.use(passport.initialize());
app.use(passport.session());
passport.serializeUser((user, cb) => cb(null, user));
passport.deserializeUser((user, cb) => cb(null, user));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const uploadMiddleware = async (req, res, next) => {
	try {
		const file = req.file;

		// Check if a file was uploaded
		if (!file) {
			return res.status(400).send('No file uploaded.');
		}

		const apiUrl = fileupload_endpoint + '/assistant/upload'

		const formData = new FormData();
		formData.append('file_upload', file.buffer, { filename: file.originalname });

		const respose = await axios.post(apiUrl, formData);

		// Respond with the response from the other API
		res.status(respose.status).send(respose.data);

	} catch (error) {
		console.error(error);
		res.status(500).send('An error occurred while uploading the file');
	}
};

app.post('/api/upload', upload.single('file'), uploadMiddleware);

// Serve static resources
app.use(express.static('./public'));

// const port_number = port || 3000
const port_number = 3000

// Start server
app.listen(port_number, () => {
	console.log(`Server listening at http://localhost:${port_number}`);
});