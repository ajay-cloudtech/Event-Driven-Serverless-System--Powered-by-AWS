import React, { useState } from 'react';
import './ResetPassword.css';

const ResetPassword = () => {
    const [email, setEmail] = useState('');
    const [otp, setOtp] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [message, setMessage] = useState('');
    const [otpSent, setOtpSent] = useState(false);

    // Dynamically set the base URL based on the environment
    const baseUrl = process.env.NODE_ENV === 'production'
        ? 'http://vehicle-service-lb-893946001.us-east-1.elb.amazonaws.com'
        : 'http://localhost:5000';

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
                setOtpSent(true); // Move to OTP and new password form
                setMessage('OTP sent to your email. Enter it below to reset your password.');
            } else {
                setMessage(data.error || 'Failed to send OTP');
            }
        } catch (error) {
            setMessage('Error: ' + error.message);
        }
    };

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
        <div className="reset-password">
            <h2>Reset Password</h2>
            
            {!otpSent ? (
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
