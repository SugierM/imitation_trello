import api from "../../services/api";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function UserProfile() {
    const [user, setUser] = useState({})
    useEffect(() => {
        getUser()
    }, [])
    const getUser = () =>{
        api.get("/users/profile/", ).then((res) => res.data).then((data) => {
            setUser(data)
            console.log(data)
        }).catch((error) => alert(error))
        
    } 
    return <div>
            <Link to="/edit_profile">Edit</Link>
            <p>Email: {user.email || "No email provided"}</p>
            <p>First name: {user.first_name || "No name provided"}</p>
            <p>Last name: {user.last_name || "No last name provided"}</p>
            <p>Bio: {user.bio || "None existent"}</p>
            <p>Nickname: {user.nickname || "No nickname provided"}</p>
            <p>Phone: {user.phone || "No phone provided"}</p>
            <img src={user.avatar} alt="Profile Image" />         
        </div>
}

export default UserProfile