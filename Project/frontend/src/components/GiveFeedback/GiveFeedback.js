import React, { useState } from 'react';
import axios from 'axios';

import './GiveFeedback.css';

function GiveFeedback() {
    const [feedback, setFeedback] = useState('');
    const [message, setMessage] = useState('');

    const username = 'samshad';

    const handleSubmit = async (e) => {
        e.preventDefault();

        const currentDateTime = new Date().toISOString().slice(0, 19).replace('T', ' ');

        const feedbackData = {
            feedback: feedback,
            username: username,
            date_time: currentDateTime
        };

        try {
            const response = await axios.post('https://mx9uotjgz8.execute-api.us-east-1.amazonaws.com/v2/feedback', feedbackData);
            if (response.status === 200) {
                setMessage('Feedback submitted successfully!');
                setFeedback('');
            } else {
                setMessage('Failed to submit feedback.');
            }
        } catch (error) {
            setMessage('Error submitting feedback.');
            console.error('Error:', error);
        }
    };

    return (
        <div className="feedbackFormContainer">
            <h1>Submit Feedback</h1>
            <form onSubmit={handleSubmit} className="feedbackForm">
                <div>
                    <label htmlFor="feedback">Feedback:</label>
                    <input
                        type="text"
                        id="feedback"
                        value={feedback}
                        onChange={(e) => setFeedback(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Submit</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
}

export default GiveFeedback;
