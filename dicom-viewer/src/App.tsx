import axios from 'axios';
import { useEffect, useState } from 'react';
import Header from './components/Header';
import ImageList from './components/ImageList';
import ImageUploader from './components/ImageUploader';


function App() {
  const [images, setImages] = useState([])
  const [changeCounter, setChangeCounter] = useState(0)

  useEffect(() => {
    axios
      .get("images")
      .then((res) => {
        setImages(res.data.map((r: string) => ({ name: r })))
      })
  }, [changeCounter])

  const imgChangeCallback = () => {
    setChangeCounter(changeCounter + 1);
  }

  return (
    <>
      <Header />
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', paddingTop: '5%' }}>
        <ImageList items={images} deleteCallback={imgChangeCallback} />
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', paddingTop: '5%' }}>
        <ImageUploader changeCallback={imgChangeCallback} />
      </div>
    </>
  );
}

export default App;
