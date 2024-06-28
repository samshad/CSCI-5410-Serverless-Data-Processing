import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './GetFeedbacks.css';

const FeedbackList = () => {
    const [feedbacks, setFeedbacks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const feedbacksPerPage = 5;

    useEffect(() => {
        const fetchFeedbacks = async () => {
            try {
                const response = await axios.get('https://2levm8ra85.execute-api.us-east-1.amazonaws.com/v1/feedbacks');
                const sortedFeedbacks = response.data.sort((a, b) => new Date(b.date_time) - new Date(a.date_time));
                setFeedbacks(sortedFeedbacks);
                setLoading(false);
            } catch (err) {
                setError(err.message);
                setLoading(false);
            }
        };

        fetchFeedbacks();
    }, []);

    const indexOfLastFeedback = currentPage * feedbacksPerPage;
    const indexOfFirstFeedback = indexOfLastFeedback - feedbacksPerPage;
    const currentFeedbacks = feedbacks.slice(indexOfFirstFeedback, indexOfLastFeedback);

    const handleNext = () => {
        if (currentPage < Math.ceil(feedbacks.length / feedbacksPerPage)) {
            setCurrentPage(currentPage + 1);
        }
    };

    const handlePrev = () => {
        if (currentPage > 1) {
            setCurrentPage(currentPage - 1);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className="feedbackListContainer">
            <h1>Feedback List</h1>
            <table className="feedbackTable">
                <thead>
                    <tr>
                        <th>Date Time</th>
                        <th>Username</th>
                        <th>Feedback</th>
                        <th>Polarity</th>
                    </tr>
                </thead>
                <tbody>
                    {currentFeedbacks.map((feedback, index) => (
                        <tr key={index}>
                            <td>{feedback.date_time}</td>
                            <td>{feedback.username}</td>
                            <td>{feedback.feedback}</td>
                            <td>{feedback.polarity}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="pagination">
                <button onClick={handlePrev} disabled={currentPage === 1}>Prev</button>
                <span>Page {currentPage} of {Math.ceil(feedbacks.length / feedbacksPerPage)}</span>
                <button onClick={handleNext} disabled={currentPage === Math.ceil(feedbacks.length / feedbacksPerPage)}>Next</button>
            </div>
        </div>
    );
};

export default FeedbackList;
