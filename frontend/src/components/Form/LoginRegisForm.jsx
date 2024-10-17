import { useEffect, useState } from "react";
import api from "../../services/api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../services/constants";
import Login from "../../pages/Login";

function LoginRegisForm({route, method}) {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [errorMessageE, setErrorMessageE] = useState("")
    const [errorMessageP, setErrorMessageP] = useState("")
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()
    const name = method === "login" ? "Login" : "Register"

    const handleSubmit = async (e) => {
        setLoading(true)
        e.preventDefault()

        try {
            const res = await api.post(route, {email, password})
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, res.data.access)
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh)
                navigate("/")
            } else {
                navigate("/login")
            }
        } catch (error) {
            if (error.response){
                setErrorMessageE(error.response.data.email || "An error occured")
                setErrorMessageP(error.response.data.password || "An error occured")
            } else {
                console.error("Error:", error.message)
                alert("Something went wrong")
            }
        } finally {
            setLoading(false)
        }
    }

    return <form onSubmit={handleSubmit} className="lr_form-container">
        <h1>{name}</h1>
        
        {errorMessageE && <p>{errorMessageE}</p>}
        {errorMessageP && <p>{errorMessageP}</p>}
        <input 
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="email@domain.pl"
            className="form-input" 
        />
        <input 
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="form-input" 
        />
        <button className="form-button" type="submit">{name}</button>

    </form>
}

export default LoginRegisForm