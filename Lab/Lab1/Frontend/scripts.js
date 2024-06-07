// API URLs for registration, login, and profile picture operations
const registrationApiUrl = 'https://k9alvyjuxd.execute-api.us-east-1.amazonaws.com/dev';
const loginApiUrl = 'https://xr169opi0f.execute-api.us-east-1.amazonaws.com/dev';
const picUploadApiUrl = 'https://0ehulb09rf.execute-api.us-east-1.amazonaws.com/dev';
const picFetchApiUrl = 'https://1rv5jddjog.execute-api.us-east-1.amazonaws.com/dev';

const img = document.getElementById('profile-picture');

// Register or login the user
async function registerOrLogin(action) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        alert("Please enter username and password.");
        return;
    }

    const apiUrl = action === 'register' ? registrationApiUrl : loginApiUrl;
    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const result = await response.json();
    if (result.statusCode === 200) {
        localStorage.setItem('username', username);
        showDashboard();
    } else {
        alert(result.body);
    }
}

// Upload the profile picture
async function uploadProfilePicture() {
    const fileInput = document.getElementById('profile-pic');
    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onloadend = async function() {
        const base64Image = reader.result.split(',')[1];
        const username = localStorage.getItem('username');

        const response = await fetch(picUploadApiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, image_data: base64Image })
        });

        const result = await response.json();
        if (result.statusCode === 200) {
            alert(result.body);
            await fetchProfilePicture();  // Fetch the uploaded picture after uploading
        } else {
            alert(result.body);
        }
    }

    reader.readAsDataURL(file);
}

// Fetch the profile picture
async function fetchProfilePicture() {
    const username = localStorage.getItem('username');
    const uploadSection = document.getElementById('upload-section');
    const profileSection = document.getElementById('picture-section');

    const response = await fetch(picFetchApiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username })
    });

    const result = await response.json();
    if (result.statusCode === 200) {
        uploadSection.style.display = 'none';
        profileSection.style.display = 'block';
        const data = JSON.parse(result.body);  // Parse the JSON body
        img.src = 'data:image/jpeg;base64,' + data.image_data;  // Set the image source
        const status = document.getElementById('img-status'); // Get the image status element
        const statusText = "Original size: " + data.image_status[1] + " ---> " +
                                "Compressed size: " + data.image_status[2]; // Set the status text
        status.textContent = statusText; // Set the image status
    } else {
        uploadSection.style.display = 'block';
        profileSection.style.display = 'none';
    }
}

// Logout the user
function logoutUser() {
    localStorage.removeItem('username');
    showAuth();  // Show login/registration page
    img.src = '';
}

// Show the dashboard
function showDashboard() {
    document.getElementById('auth').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';

    const userNameElement = document.getElementById('user-name');
    userNameElement.textContent = localStorage.getItem('username');

    fetchProfilePicture();
}

// Show the authentication section
function showAuth() {
    document.getElementById('auth').style.display = 'block';
    document.getElementById('dashboard').style.display = 'none';
}

// Initialize the page
if (localStorage.getItem('username')) {
    showDashboard();
} else {
    showAuth();
}
