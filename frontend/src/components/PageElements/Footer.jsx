import "./css/HeaderFooter.css"

function Footer(){

    return(
        <footer className="footer">
            &copy; This is just for learning purposes {new Date().getFullYear()} 
            <span><a href="https://github.com/SugierM/imitation_trello"><b> https://github.com/SugierM/imitation_trello</b></a></span>
        </footer>
    );
}

export default Footer