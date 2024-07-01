import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Button, Pagination } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import './GetFeedbacks.css';

/**
 * GetFeedbacks Component
 * This component fetches and displays a list of feedbacks with pagination.
 * Users can delete feedback as well.
 */
const FeedbackList = () => {
    const [feedbacks, setFeedbacks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const feedbacksPerPage = 5; // Number of feedbacks to display per page

    /**
     * Fetch feedbacks from the API and sort them by date in descending order.
     * This function is called when the component is mounted.
     * 
     * @returns {Promise<void>}
     * 
     * @see {@link https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort} Array.prototype.sort()
     * @see {@link https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date} Date
     */
    const fetchFeedbacks = async () => {
        setLoading(true);
        try {
            const response = await axios.get('https://2levm8ra85.execute-api.us-east-1.amazonaws.com/v1/feedbacks');
            const sortedFeedbacks = response.data.sort((a, b) => new Date(b.date_time) - new Date(a.date_time));
            setFeedbacks(sortedFeedbacks);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFeedbacks();
    }, []);

    /**
     * Get the current feedbacks to display based on the current page.
     * @see {@link https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/slice} Array.prototype.slice()
     */
    const indexOfLastFeedback = currentPage * feedbacksPerPage;
    const indexOfFirstFeedback = indexOfLastFeedback - feedbacksPerPage;
    const currentFeedbacks = feedbacks.slice(indexOfFirstFeedback, indexOfLastFeedback);

    /**
     * Handle pagination to the next page.
     * @see {@link https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/ceil} Math.ceil()
     */
    const handleNext = () => {
        if (currentPage < Math.ceil(feedbacks.length / feedbacksPerPage)) {
            setCurrentPage(currentPage + 1);
        }
    };

    /**
     * Handle pagination to the previous page.
     */
    const handlePrev = () => {
        if (currentPage > 1) {
            setCurrentPage(currentPage - 1);
        }
    };

    /**
     * Handle pagination to the first page.
     */
    const handleFirst = () => {
        setCurrentPage(1);
    };

    /**
     * Handle pagination to the last page.
     */
    const handleLast = () => {
        setCurrentPage(Math.ceil(feedbacks.length / feedbacksPerPage));
    };

    /**
     * Handle the deletion of a feedback.
     * @param {string} feedback_id - The ID of the feedback to delete.
     * @returns {Promise<void>}
     */
    const handleDelete = async (feedback_id) => {
        try {
            await axios.post('https://2levm8ra85.execute-api.us-east-1.amazonaws.com/v1/delete_feedbacks', { feedback_id });
            // Remove the deleted feedback from the state
            setFeedbacks(feedbacks.filter(feedback => feedback.feedback_id !== feedback_id));
        } catch (err) {
            console.error('Error deleting feedback:', err.message);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className="feedbackListContainer">
            <h1>Feedback List</h1>
            <Button onClick={fetchFeedbacks} className="mb-3">Refresh</Button>
            <Table striped bordered hover className="feedbackTable">
                <thead>
                    <tr>
                        <th>Date Time</th>
                        <th>Username</th>
                        <th>Feedback</th>
                        <th>Polarity</th>
                        <th>Delete Feedback</th>
                    </tr>
                </thead>
                <tbody>
                    {currentFeedbacks.map((feedback, index) => (
                        <tr key={index}>
                            <td>{new Date(feedback.date_time).toLocaleString()}</td>
                            <td>{feedback.username}</td>
                            <td>{feedback.feedback}</td>
                            <td>{feedback.polarity}</td>
                            <td>
                                <Button variant="danger" onClick={() => handleDelete(feedback.feedback_id)}>Delete</Button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
            <Pagination className="justify-content-center">
                <Pagination.First onClick={handleFirst} disabled={currentPage === 1} />
                <Pagination.Prev onClick={handlePrev} disabled={currentPage === 1} />
                <Pagination.Item active>{currentPage}</Pagination.Item>
                <Pagination.Next onClick={handleNext} disabled={currentPage === Math.ceil(feedbacks.length / feedbacksPerPage)} />
                <Pagination.Last onClick={handleLast} disabled={currentPage === Math.ceil(feedbacks.length / feedbacksPerPage)} />
            </Pagination>
        </div>
    );
};

export default FeedbackList;
