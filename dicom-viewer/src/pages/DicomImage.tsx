import axios from 'axios';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/joy/Button';
import { useEffect, useState } from 'react';
import Header from '../components/Header';
import TagList from '../components/TagList';



function DicomImage() {
  const [tags, setTags] = useState([])
  const [search, setSearch] = useState('')
  let hash = window.location.hash;
  let imgNameFrags = hash.split('/');
  let imgName = imgNameFrags[imgNameFrags.length - 1]

  useEffect(() => {
    axios.get("images/" + imgName + "/tags")
      .then((res) => {
        setTags(res.data)
      })
  }, [])


  const handleSearch = (e: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
    setSearch(e.target.value)
  }
  const searchTags = () => {
    axios.get("images/" + imgName + "/tags?search=" + search)
      .then((res) => { setTags(res.data) })
  }

  return (
    <>
      <Header />
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', paddingTop: '5%' }}>
        <h1>
          {imgName}
        </h1>
        <img width={250} height={250} src={"/images/" + imgName + "?png=true"} alt={imgName} />
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', paddingTop: '5%' }}>
        <h2>Search Tags</h2>
        <br />
        <Box component="form" sx={{ '& > :not(style)': { m: 1, width: '25ch' } }} noValidate autoComplete="off">
          <TextField id="standard-basic" label="Standard" variant="standard" onChange={handleSearch} />
          <Button onClick={searchTags}>Search</Button>
        </Box>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', paddingTop: '5%' }}>
        <TagList tags={tags} />
      </div>
    </>
  );
}

export default DicomImage;
