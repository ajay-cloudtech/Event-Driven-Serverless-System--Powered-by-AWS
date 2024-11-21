import React, { useState } from 'react';
import './ResetPassword.css';

//main reset password function to take user input and sends it to backend
const ResetPassword = () => {
    const [email, setEmail] = useState('');
    const [otp, setOtp] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [message, setMessage] = useState('');
    const [otpSent, setOtpSent] = useState(false);

    // set the url to local or prod based on the environment dynamically
    const baseUrl = process.env.NODE_ENV === 'production'
        ? 'http://vehicle-service-lb-893946001.us-east-1.elb.amazonaws.com'
        : 'http://localhost:5000';

    // send otp and display message on request reset password form submission
    const handleSendOtp = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${baseUrl}/forgot-password`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email }),
            });

            const data = await response.json();
            if (response.ok) {
                setOtpSent(true); // redirect to OTP and new password form
                setMessage('OTP sent to your email. Enter it below to reset your password.');
            } else {
                setMessage(data.error || 'Failed to send OTP');
            }
        } catch (error) {
            setMessage('Error: ' + error.message);
        }
    };

    // accept and send new password and OTP verification to backend
    const handleResetPassword = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${baseUrl}/reset-password`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, otp, newPassword }),
            });

            const data = await response.json();
            if (response.ok) {
                setMessage('Password reset successfully. You can now log in with your new password.');
            } else {
                setMessage(data.error || 'Failed to reset password');
            }
        } catch (error) {
            setMessage('Error: ' + error.message);
        }
    };

    return (
        //html component for reset-password page
        <div className="reset-password">
            <h2>Reset Password</h2>
            
            {!otpSent ? (
                //form for requesting reset password
                <form onSubmit={handleSendOtp}>
                    <div>
                        <label>Email:</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit">Send OTP</button>
                </form>
            ) : (
                //form for submitting new password
                <form onSubmit={handleResetPassword}>
                    <div>
                        <label>OTP Code:</label>
                        <input
                            type="text"
                            value={otp}
                            onChange={(e) => setOtp(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <label>New Password:</label>
                        <input
                            type="password"
                            value={newPassword}
                            onChange={(e) => setNewPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit">Reset Password</button>
                    <p><a href='/login'>Login</a></p>
                </form>
            )}
            
            {message && <p>{message}</p>}
        </div>
    );
};

export default ResetPassword;
