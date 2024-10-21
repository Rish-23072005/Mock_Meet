import React, { useState } from 'react';
import { BsFillGearFill } from 'react-icons/bs';
import { TextField, Button, FormControl, FormLabel, RadioGroup, FormControlLabel, Radio } from '@material-ui/core';

function Settings() {
  const [theme, setTheme] = useState('light');
  const [language, setLanguage] = useState('english');

  const handleThemeChange = (event) => {
    setTheme(event.target.value);
  };

  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Settings saved!');
  };

  return (
    <main className='main-container'>
      <div className='main-title'>
        <h3 className='alpha'>SETTINGS</h3>
        <BsFillGearFill />
      </div>

      <form onSubmit={handleSubmit}>
        <FormControl component="fieldset">
          <FormLabel component="legend">Theme</FormLabel>
          <RadioGroup aria-label="theme" name="theme" value={theme} onChange={handleThemeChange}>
            <FormControlLabel value="light" control={<Radio />} label="Light" />
            <FormControlLabel value="dark" control={<Radio />} label="Dark" />
          </RadioGroup>
        </FormControl>

        <FormControl component="fieldset">
          <FormLabel component="legend">Language</FormLabel>
          <RadioGroup aria-label="language" name="language" value={language} onChange={handleLanguageChange}>
            <FormControlLabel value="english" control={<Radio />} label="English" />
            <FormControlLabel value="spanish" control={<Radio />} label="Spanish" />
            <FormControlLabel value="french" control={<Radio />} label="French" />
          </RadioGroup>
        </FormControl>

        <TextField id="api-key" label="API Key" variant="outlined" />

        <Button variant="contained" color="primary" type="submit">
          Save Settings
        </Button>
      </form>
    </main>
  );
}

export default Settings;