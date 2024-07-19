import React, { useState } from 'react';
import axios from 'axios';
import { Form, Button, Container, Alert } from 'react-bootstrap';

import './GiveFeedback.css';

/**
 * GiveFeedback Component
 * This component allows users to submit their feedback.
 * The feedback is then stored in the database.
 */
function GiveFeedback() {
    const [feedback, setFeedback] = useState('');
    const [message, setMessage] = useState('');

    const username = 'samshad';  // TODO: need to make it dynamic. For now, hardcoding it.

    /**
     * Handles the form submission for feedback.
     * @param {object} e - The event object
     * @returns {Promise<void>}
     */
    const handleSubmit = async (e) => {
        e.preventDefault();

        // Get the current date and time in ISO format
        const currentDateTime = new Date().toISOString().slice(0, 19).replace('T', ' ');

        // Prepare feedback data/payload in JSON format
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
        <Container className="feedbackFormContainer">
            <h1>Submit Feedback</h1>
            <Form onSubmit={handleSubmit} className="feedbackForm">
                <Form.Group controlId="feedback">
                    <Form.Label>Feedback:</Form.Label>
                    <Form.Control
                        as="textarea"
                        rows={5}
                        value={feedback}
                        onChange={(e) => setFeedback(e.target.value)}
                        required
                    />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
            {message && <Alert variant={message.includes('successfully') ? 'success' : 'danger'}>{message}</Alert>}
        </Container>
    );
}

export default GiveFeedback;
