import { Link } from "react-router-dom";

function Header(){
    const style = {
        display: "inline-block",
        margin: "0px 10px 0px 0px",
    }

    return(
<nav className="navbar navbar-expand-lg bg-body-tertiary">
        <span className="fs-2 text fw-bold" style={{margin: "5px 5px 5px 20px"}}>Imitationer</span>
  <div className="container-fluid">
    
    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span className="navbar-toggler-icon"></span>
    </button>
    <div className="collapse navbar-collapse" id="navbarNav">
      <ul className="navbar-nav">

        <li className="nav-item" style={{margin: "10px 8px 10px 8px"}}>
            <Link to="/" className="nav-link active" aria-current="page">Docs</Link>
        </li>
        <li className="nav-item" style={{margin: "10px 8px 10px 8px"}}>
          <Link to="/boards" className="nav-link active" aria-current="page">Boards</Link>
        </li>
        <li className="nav-item" style={{margin: "10px 8px 10px 8px"}}>
        <Link to="/profile" className="nav-link active" aria-current="page">Profile</Link>
        </li>
        <li className="nav-item" style={{margin: "10px 8px 10px 8px"}}>
        <Link to="/search_user" className="nav-link active" aria-current="page">Search users</Link>
        </li>
        <li className="nav-item" style={{margin: "10px 8px 10px 8px"}}>
          <Link to="/boards" className="nav-link active" aria-current="page">Dashboard - (now boards)</Link>
        </li>

      </ul>
    </div>
  </div>
</nav>
    );
}

export default Header