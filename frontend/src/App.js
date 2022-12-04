// @ts-nocheck

import { useState } from "react";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";

function App() {
  const [word, setWord] = useState("");
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    console.log(word);
    setLoading(false);
  }

  return (
    <div style={{ flexGrow: 1 }}>
      <Grid
        container
        spacing={0}
        direction="column"
        alignItems="center"
        justifyContent="center"
        style={{ minHeight: "100vh" }}
      >
        <form onSubmit={handleSubmit}>
          <Grid item xs={12} sm={6}>
            <TextField
              value={word}
              label={"Interesting Words"}
              onInput={(e) => setWord(e.target.value)}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <div style={{ marginTop: "20px" }}>
              <Button fullWidth variant="contained" type="submit">
                Question Generator
              </Button>
            </div>
          </Grid>
        </form>
      </Grid>
    </div>
  );
}

export default App;
