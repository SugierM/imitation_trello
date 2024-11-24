import "./css/CardSearch.css";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function CardBoards({ board, creator }) {
    const [url, setUrl] = useState("");
    const navigate = useNavigate();

    return (
        <div className="card" style={{width: "18rem", height: "280px", margin: "6px 5px 6px 5px"}}>
            <div className="card-body">
                <h5 className="card-title"><Link to={`/boards/${board.pk}`}>{board.name}</Link></h5>
                <p className="card-text">Description: {board.description || "No description"}</p>
                <div style={{position: "absolute", bottom: 0}}>
                    <p href="#" className="btn btn-primary"><Link to={`/otherprofile/${creator}`} style={{color: "white"}}>Creator</Link></p>
                </div>
            </div>
        </div>
    );
}

export default CardBoards;
