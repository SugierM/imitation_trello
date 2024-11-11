import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import CardBoards from '../components/PageElements/CardBoards';

function OtherProfile() {
  const { url } = useParams();
  const [data, setData] = useState({});
  const [boards, setBoards] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const path = new URL(url).pathname;
        const response = await api.get(decodeURIComponent(path));
        setData(response.data);
        setBoards(response.data.boards || []);
      } catch (error) {
        console.error("Error fetching data", error);
      }
    };
    fetchData();
  }, [url]);

  return (
    <div>
        <p>Email: {data.email || "No email provided"}</p>
        <p>First name: {data.first_name || "No name provided"}</p>
        <p>Last name: {data.last_name || "No last name provided"}</p>
        <p>Bio: {data.bio || "None existent"}</p>
        <p>Nickname: {data.nickname || "No nickname provided"}</p>
        <p>Phone: {data.phone || "No phone provided"}</p>
        
        <div>
            <h2>Common boards</h2>
            {boards.length > 0 ? (
                boards.map((board) => (
                    <CardBoards board={board} PUrl={board.creator.url} />
                ))
            ) : (
                <p>No common boards</p>
            )}
        </div>
    </div>
  );
}

export default OtherProfile;
