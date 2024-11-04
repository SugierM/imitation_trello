import api from "../services/api";
import { useEffect, useState } from "react";
import Header from "../components/Header/Header";

function UserSearchForm(){
    const [searchTerm, setSearchTerm] = useState("");
    const [result, setResult] = useState({ count: 0, next: null, previous: null, results: [] });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleInput = (e) => {
        setSearchTerm(e.target.value);
    };

    const fetchResults = async (url) => {
        setLoading(true);
        setError(null);

        try {
            const response = await api.get(url);
            console.log(response);
            setResult(response.data);
        } catch (err) {
            setError("Failed to get users");
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        fetchResults(`/users/search_user/?q=${searchTerm}`);
    };

    const handleNextPage = () => {
        if (result.next) {
            fetchResults(result.next);
        }
    };

    const handlePreviousPage = () => {
        if (result.previous) {
            fetchResults(result.previous);
        }
    };

    return (
        <div>
            <Header></Header>
            <h2>Search Users</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" value={searchTerm} onChange={handleInput} placeholder="Search users"/>
                <button type="submit">Search</button>
            </form>

            {loading && <p>Loading...</p>}
            {error && <p style={{color: "red"}}>{error}</p>}

            <div>
                {result.results.length > 0 ? (
                    <ul>
                        {result.results.map((user) => (
                            <li>
                                {user.email}
                            </li>
                        ))}
                    </ul>
                ) : !loading && <p>No users found</p>}
            </div>

            <div>
                <button onClick={handlePreviousPage} disabled={!result.previous}>Previous</button>
                <button onClick={handleNextPage} disabled={!result.next}>Next</button>
            </div>
        </div>
    );
}

export default UserSearchForm;