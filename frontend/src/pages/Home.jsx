import api from "../services/api"
import { useState, useEffect } from "react"


function Home() {
    const [currentUser, setCurrentUser] = useState([])
    const [content, setContent] = useState("")

    useEffect(() => {
        getUser()
    }, [])

    const getUser = () => {
        api.get("users/user/")
            .then((res) => res.data)
            .then((data) => {setCurrentUser(data), console.log(data)})
            .catch((error) => alert(erorr))
    }
}

export default Home