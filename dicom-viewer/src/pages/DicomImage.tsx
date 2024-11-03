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
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        PNG Version:
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <img width={250} height={250} src={"/images/" + imgName + "?png=true"} alt={imgName} />
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', paddingTop: '5%' }}>
        <h2>Filter Tags</h2>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Box component="form" sx={{ '& > :not(style)': { m: 1, width: '25ch' } }} noValidate autoComplete="off">
          <TextField id="standard-basic" label="e.g. 0010, or ,0010" variant="standard" onChange={handleSearch} />
          <Button onClick={searchTags}>Apply Filter</Button>
        </Box>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <TagList tags={tags} />
      </div>
    </>
  );
}

export default DicomImage;
