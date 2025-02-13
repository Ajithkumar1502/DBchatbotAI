import React, { useState } from "react";
import axios from "axios";
import { Container, TextField, Button, Typography, List, ListItem } from "@mui/material";

const App = () => {
    const [query, setQuery] = useState("");
    const [response, setResponse] = useState([]);
    
    const sendQuery = async () => {
        if (!query.trim()) return;
        const { data } = await axios.get(`http://127.0.0.1:8000/query/?query=${query}`);
        setResponse([...response, { query, reply: data.response }]);
        setQuery("");
    };

    return (
        <Container>
            <Typography variant="h4" sx={{ mt: 4 }}>AI Chatbot</Typography>
            <TextField 
                label="Ask something..." 
                fullWidth 
                value={query} 
                onChange={(e) => setQuery(e.target.value)} 
                sx={{ my: 2 }} 
            />
            <Button variant="contained" color="primary" onClick={sendQuery}>Send</Button>
            <List>
                {response.map((item, index) => (
                    <ListItem key={index}>
                        <Typography variant="body1"><strong>You:</strong> {item.query}</Typography>
                        <Typography variant="body2"><strong>Bot:</strong> {item.reply}</Typography>
                    </ListItem>
                ))}
            </List>
        </Container>
    );
};

export default App;
