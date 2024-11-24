import api from "./api";

const fetchList = async (url, setList, setNextUrl, setPrevUrl, fetchTypes) => {
    try {
        const response = await api.get(url);
        setList(response.data.results);
        setNextUrl(response.data.next);
        setPrevUrl(response.data.previous);
    } catch (error) {
        console.error(`Error fetching ${fetchTypes}:`, error);
        setError(`Failed to load ${fetchTypes}.`);
    }
};

export default fetchList