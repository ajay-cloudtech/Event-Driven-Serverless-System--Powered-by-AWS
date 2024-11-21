import React, { useEffect, useState } from 'react';
import './Reports.css';
import ReactJson from 'react-json-pretty';
import 'react-json-pretty/themes/monikai.css';


const Reports = () => {
    const [reports, setReports] = useState([]); 
    const [reportContent, setReportContent] = useState(null);
    const [error, setError] = useState(null); 
   // const userId = 'ajaytest1'; 

    // set the url to local or prod based on the environment dynamically
    const baseUrl = process.env.NODE_ENV === 'production'
        ? 'http://vehicle-service-lb-893946001.us-east-1.elb.amazonaws.com'
        : 'http://localhost:5000';

    useEffect(() => {
        const fetchReports = async () => {
            const storedUserId = localStorage.getItem('userId'); // get user id from local storage
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
    }, []); 

    // fetch the content of the selected report
    const fetchReportContent = async (reportName) => {
        console.log("Fetching report:", reportName);
        try {
            const response = await fetch(`${baseUrl}/api/reports/${reportName.split('/').pop()}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const reportData = await response.json();
            console.log("Fetched report data:", reportData);
            setReportContent(reportData); 
        } catch (err) {
            console.error("Error fetching report content:", err);
            setError('Failed to fetch report content');
        }
    };

    const renderReportContent = () => {
        if (typeof reportContent === 'object') {
            // render as JSON if the content is an object
            return <ReactJson src={reportContent} theme="monikai" />;
        } else if (typeof reportContent === 'string') {
            // render as plain text if the content is a string
            return <pre>{reportContent}</pre>;
        }
        return null;
    };

    return (
        //html component for displaying reports 
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
                            {renderReportContent()} {/* render report based on content type */}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Reports;
