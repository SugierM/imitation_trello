import { Link } from "react-router-dom";

function Header(){
    const style = {
        display: "inline-block",
        margin: "0px 10px 0px 0px",
    }

    return(
        <header>
            <h1 style={style}>Imitationer</h1>
            <ul>
                <li style={style}><Link to="/">Home</Link></li>
                <li style={style}><Link to="/boards">Boards</Link></li>
                <li style={style}><Link to="/profile">Profile</Link></li>
                <li style={style}><Link to="/search_user">Search users</Link></li>
            </ul>
        </header>
    );
}

export default Header