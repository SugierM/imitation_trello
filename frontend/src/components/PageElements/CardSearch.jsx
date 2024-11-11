import  "./css/CardSearch.css"


function CardSearch({email, nickname, last_name, first_name, url, urlFunction}){
    return (
        <div className="card">
            <div className="card-title">
                <h2>{nickname || first_name}</h2>
            </div>
            <div className="card-content">
                <p>Email: {email}</p>
                <p>Name: {first_name || ""}</p>
                <p>Last name: {last_name || ""}</p>
                <button onClick={() => urlFunction(url)}>Profile</button>
            </div>
        </div>
    )
}

export default CardSearch