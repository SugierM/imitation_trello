import React, { useState, useEffect } from 'react';
import api from "../services/api";
function UserEditForm() {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        bio: '',
        nickname: '',
        phone: ''
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                setLoading(true);
                const response = await api.get("/users/profile/");
                setFormData(response.data);
            } catch (err) {
                setError("Failed to load user data.");
                console.error("Error fetching user data:", err);
            } finally {
                setLoading(false);
            }
        };
        
        fetchUserData();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevFormData) => ({
            ...prevFormData,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.patch("/users/profile/", formData);
            alert("Profile updated successfully!");
        } catch (err) {
            alert("Failed to update profile. Please try again.");
            console.error("Error updating profile:", err);
        }
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p style={{ color: "red" }}>{error}</p>;

    return (
        <div>
            <h2>Edit User</h2>
            <form onSubmit={handleSubmit}>
                
                <div>
                    <label>First Name:</label>
                    <input
                        type="text"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleChange}
                    />
                </div>

                <div>
                    <label>Last Name:</label>
                    <input
                        type="text"
                        name="last_name"
                        value={formData.last_name}
                        onChange={handleChange}
                    />
                </div>

                <div>
                    <label>Bio:</label>
                    <textarea
                        name="bio"
                        value={formData.bio}
                        onChange={handleChange}
                    />
                </div>

                <div>
                    <label>Nickname:</label>
                    <input
                        type="text"
                        name="nickname"
                        value={formData.nickname}
                        onChange={handleChange}
                    />
                </div>

                <div>
                    <label>Phone:</label>
                    <input
                        type="tel"
                        name="phone"
                        value={formData.phone}
                        onChange={handleChange}
                    />
                </div>

                <button type="submit">Save</button>
            </form>
        </div>
    );
}

export default UserEditForm;
