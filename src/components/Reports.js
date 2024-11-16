import React, { useEffect, useState } from 'react';
import './Reports.css';
import ReactJson from 'react-json-pretty';
import 'react-json-pretty/themes/monikai.css';

const Reports = () => {
    const [reports, setReports] = useState([]); // List of report filenames
    const [reportContent, setReportContent] = useState(null); // Content of the selected report
    const [error, setError] = useState(null); // For error handling
    const userId = 'ajaytest1'; // Replace this with actual user ID as needed

    // Dynamically set the base URL based on the environment
    const baseUrl = process.env.NODE_ENV === 'production'
        ? 'http://vehicle-service-lb-893946001.us-east-1.elb.amazonaws.com'
        : 'http://localhost:5000';

    useEffect(() => {
        const fetchReports = async () => {
            const storedUserId = localStorage.getItem('userId'); // Get user ID from local storage
            if (!storedUserId) {
                setError('User ID is not found. Please log in again.');
                return;
            }
    
            try {
                const response = await fetch(`${baseUrl}/api/reports?user_id=${storedUserId}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                console.log("Fetched reports:", data);
                setReports(data);
            } catch (err) {
                console.error("Error fetching reports:", err);
                setError('Failed to fetch reports');
            }
        };
    
        fetchReports();
    }, []); // No dependency on userId, it's fetched from local storage

    // Fetch the content of the selected report
    const fetchReportContent = async (reportName) => {
        console.log("Fetching report:", reportName);
        try {
            const response = await fetch(`${baseUrl}/api/reports/${reportName.split('/').pop()}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const reportData = await response.json();
            console.log("Fetched report data:", reportData);
            setReportContent(reportData); // Set the content for rendering
        } catch (err) {
            console.error("Error fetching report content:", err);
            setError('Failed to fetch report content');
        }
    };

    const renderReportContent = () => {
        if (typeof reportContent === 'object') {
            // Render as JSON if the content is an object
            return <ReactJson src={reportContent} theme="monikai" />;
        } else if (typeof reportContent === 'string') {
            // Render as plain text if the content is a string
            return <pre>{reportContent}</pre>;
        }
        return null;
    };

    return (
        <div className="reports-container">
            <h2>Vehicle Maintenance Reports</h2>
            {error && <p className="error">{error}</p>}
            <div className="reports-content">
                <div className='rl'>
                    <ul className="reports-list">
                        {Array.isArray(reports) && reports.length > 0 ? (
                            reports.map((report) => (
                                <li key={report}>
                                    <button onClick={() => fetchReportContent(report)}>
                                        {report}
                                    </button>
                                </li>
                            ))
                        ) : (
                            <p>Loading...</p>
                        )}
                    </ul>
                </div>
                <div className='rc'>
                    {reportContent && (
                        <div className="report-content">
                            <h3>Report Content:</h3>
                            {renderReportContent()} {/* Render report based on content type */}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Reports;
