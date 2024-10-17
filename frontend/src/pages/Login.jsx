import LoginRegisForm from "../components/Form/LoginRegisForm"

function Login() {
    return <LoginRegisForm route="api/token/" method="login" />
}

export default Login