import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import UserProfile from "./pages/Users/UserProfile"
import Home from "./pages/Home"
import NotAuthorized from "./pages/NotAuthorized"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute"
import UserSearchForm from "./pages/Users/SearchUserForm"
import UserEditForm from "./pages/Users/UserEdit"
import OtherProfile from "./pages/Users/OtherProfile"
import Boards from "./pages/Boards/Boards"
import BoardsDetail from "./pages/Boards/BoardsDetail"
import BoardCreate from "./pages/Boards/BoardsCreate"
import ElementsDetail from "./pages/Elements/ElementsDetail"


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
        <Route path="/edit_profile" element={<ProtectedRoute><UserEditForm /></ProtectedRoute>}></Route>
        <Route path="/search_user" element={<ProtectedRoute><UserSearchForm /></ProtectedRoute>}></Route>
        <Route path="/otherprofile/:url" element={<ProtectedRoute><OtherProfile /></ProtectedRoute>}></Route>

        <Route path="/boards/:pk" element={<ProtectedRoute><BoardsDetail /></ProtectedRoute>}></Route>
        <Route path="/boards" element={<ProtectedRoute><Boards /></ProtectedRoute>}></Route>
        <Route path="/boards/create" element={<ProtectedRoute><BoardCreate /></ProtectedRoute>}></Route>

        <Route path="/element/:pk" element={<ProtectedRoute><ElementsDetail /></ProtectedRoute>}></Route>

        <Route path="/not_auth" element={<ProtectedRoute><NotAuthorized /></ProtectedRoute>}></Route>
        <Route path="*" element={<NotFound />}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
