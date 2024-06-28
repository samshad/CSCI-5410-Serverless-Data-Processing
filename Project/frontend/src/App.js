import React from 'react';
import { Link, Route, Routes } from 'react-router-dom';

import { Navbar, Nav } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import Home from './pages/Home';
import SubmitFeedback from './pages/SubmitFeedback';
import FeedbackList from './pages/FeedbackList';

// import './App.css';

function App() {
  return (
    <>
      <Navbar bg="light" expand="lg">
        <Navbar.Brand as={Link} to="/">Feedback App</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link as={Link} to="/">Home</Nav.Link>
            <Nav.Link as={Link} to="/give_feedback">Submit Feedback</Nav.Link>
            <Nav.Link as={Link} to="/get_feedback">Feedback List</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/give_feedback" element={<SubmitFeedback />} />
        <Route path="/get_feedback" element={<FeedbackList />} />
      </Routes>
    </>
  );
}

export default App;
