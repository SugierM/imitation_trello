import "./css/CardSearch.css";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function CardBoards({ board, PUrl }) {
    const [url, setUrl] = useState("");
    const [creator, setCreator] = useState({});
    const navigate = useNavigate();

    useEffect(() => {
        setUrl(PUrl);
        setCreator(board.creator); 
    }, [board]);

    const UserProfileButton = () => {
        const otherProfileUrl = encodeURIComponent(url);
        navigate(`/otherprofile/${otherProfileUrl}`);
    };

    const BoardDetail = () => {
        navigate(`/boards/${board.pk}`)
    }

    return (
        <div className="card">
            <div className="card-title">
                <Link to={`/boards/${board.pk}`}><h2>{board.name}</h2></Link>
            </div>
            <div className="card-content">
                <p>Description: {board.description || "No description"}</p>
                <p>Status: {board.status === 0 ? "Ongoing" : "Done"}</p>
                <button onClick={UserProfileButton}>Creator</button>
            </div>
        </div>
    );
}

export default CardBoards;
