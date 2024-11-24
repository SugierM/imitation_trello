import React, { useEffect, useState } from 'react'
import api from '../../services/api'
import CardBoards from '../../components/PageElements/CardBoards'
import { Link } from 'react-router-dom';

function Boards() {
    const [searchTerm, setSearchTerm] = useState('');
    const [boards, setBoards] = useState({ results: [], next: null, previous: null });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(()=>{
        getBoards()
    }, [])

    const getBoards = () => {
        api.get("boards/boards_list/")
        .then((response) => response.data)
        .then((data) => setBoards(data))
        .catch((error) => {alert(error)})
    }

    const handleNextPage = () => {
        if (boards.next) {
            fetchResults(boards.next);
        }
    };

    const handlePreviousPage = () => {
        if (boards.previous) {
            fetchResults(boards.previous);
        }
    };

    return (
        <div>
            {error && <p>{error}</p>}
            <Link to={"/boards/create"}>Create</Link>
            <hr />
            <div style={{margin: "0px 0px 40px 30px"}}>
                {boards.results.length > 0 ? (
                    boards.results.map((board, index) => (
                        <CardBoards
                            key={index}
                            board={board}
                            creator={board.board_creator}
                        />
                    ))
                ) : (
                    !loading && <p>No boards found.</p>
                )}
            </div>

            <div className="pagination-controls">
                <button onClick={handlePreviousPage} disabled={!boards.previous}>Previous</button>
                <button onClick={handleNextPage} disabled={!boards.next}>Next</button>
            </div>
        </div>
    );
}

export default Boards;