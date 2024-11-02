import axios from 'axios';
import Button from '@mui/joy/Button';
import { useState } from "react";

const ImageUploader = ({ changeCallback }: { changeCallback: () => void }) => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);

  const onFileUpload = () => {
    const formData = new FormData();

    if (selectedImage != null) {
      formData.append("file", selectedImage);
    }

    axios.post("images", formData, { headers: { "Content-Type": "multipart/form-data" } })
      .then(() => changeCallback())
  }

  return (
    <div>
      <input type="file" name="dicomImage" onChange={
        (event) => setSelectedImage(event.target.files ? event.target.files[0] : null)
      } />
      {selectedImage && (
        <Button color="danger" onClick={() => setSelectedImage(null)}>Remove</Button>
      )}
      <Button sx={{ mx: '5px' }} onClick={onFileUpload}>Upload</Button>
    </div >
  )
}

export default ImageUploader;
