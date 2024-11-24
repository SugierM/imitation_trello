import api from "../../services/api";
import { useEffect, useState } from "react";
import CardSearch from "../../components/PageElements/CardSearch";



function UserSearchForm(){
    const [searchTerm, setSearchTerm] = useState("");
    const [result, setResult] = useState({ count: 0, next: null, previous: null, results: [] });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [otherUrl, setOtherUrl] = useState("")


    const handleInput = (e) => {
        setSearchTerm(e.target.value);
    };

    const fetchResults = async (url) => {
        setLoading(true);
        setError(null);

        try {
            const response = await api.get(url);
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

    const UserProfileButton = (pUrl) => {
        setOtherUrl(pUrl)
        const url = encodeURIComponent(pUrl)
        window.open(`/otherprofile/${url}`)
    }

    return (
        <div>
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
                            <CardSearch
                                nickname={user.nickname}
                                email={user.email}
                                first_name={user.first_name}
                                last_name={user.last_name}
                                urlFunction={() => UserProfileButton(user.pk)}
                            />
                        ))}
                    </ul>
                ) : !loading && <p>No users found</p>}
            </div>

            <div style={{margin: "0px 0px 80px 0px"}}>
                <button onClick={handlePreviousPage} disabled={!result.previous}>Previous</button>
                <button onClick={handleNextPage} disabled={!result.next}>Next</button>
            </div>
        </div>
    );
}

export default UserSearchForm;