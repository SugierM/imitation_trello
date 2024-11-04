import api from "../services/api"
import { useState, useEffect } from "react"


function Home() {
    // const [currentUser, setCurrentUser] = useState([])
    // const [content, setContent] = useState("")

    // useEffect(() => {
    //     getUser()
    // }, [])

    // const getUser = () => {
    //     api.get("users/profile/")
    //         .then((res) => res.data)
    //         .then((data) => {setCurrentUser(data), console.log(data)})
    //         .catch((error) => alert(erorr))
    // }
    return <div>
        <span>UI for backend</span>
        <div>
            For now there are few calls that can be made
            <ul>
                Users - starts with /users/
                <li>create_user/</li>
                <li>search_user/</li>
                <li>profile/</li>
                <li>retr_user/int/</li>
                <li>profile_destroy/</li>
            </ul>
            <ul>
                And the rest for now is under - /boards/ <br />
                Boards
                <li>boards_create/</li>
                <li>boards_destroy/int/</li>
                <li>boards/int/</li>
                <li>boards_list/</li>
                Elements
                <li>elements/int/</li>
                <li>elements_create/</li>
                <li>elements_destroy/int/</li>
                <li>elements_list/int/</li>
                Tasks
                <li>tasks/int/</li>
                <li>tasks_create/</li>
                <li>tasks_list/int/</li>
                <li>task_destroy/int/</li>
            </ul>
        </div>
    </div>
}

export default Home