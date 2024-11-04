import Header from "./components/Header/Header"
import Footer from "./components/Footer/Footer"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import UserProfile from "./pages/UserProfile"
import Home from "./pages/Home"
import NotAuthorized from "./pages/NotAuthorized"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute"
import UserSearchForm from "./pages/SearchUserForm"
import UserEditForm from "./pages/UserEdit"


function Logout(){
  localStorage.clear()
  return <Navigate to="/login"/>
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>}></Route>
        <Route path="/login" element={<Login />}></Route>
        <Route path="/logout" element={<Logout />}></Route>
        <Route path="/register" element={<Register />}> </Route>
        <Route path="/profile" element={<ProtectedRoute><UserProfile /></ProtectedRoute>}></Route>
        <Route path="/search_user" element={<ProtectedRoute><UserSearchForm /></ProtectedRoute>}></Route>
        <Route path="/edit_profile" element={<ProtectedRoute><UserEditForm /></ProtectedRoute>}></Route>
        <Route path="*" element={<NotFound />}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
