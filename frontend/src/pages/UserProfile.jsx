import api from "../services/api";
import { useEffect, useState } from "react";

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
            <p>Email: {user.email || "No email provided"}</p>
            <p>Bio: {user.bio || "None existent"}</p>
            <p>Nickname: {user.nickname || "No nickname provided"}</p>
            <p>Phone: {user.phone || "No phone provided"}</p>
        </div>

}

export default UserProfile