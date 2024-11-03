import axios from 'axios';
import * as React from 'react';
import { Link } from "react-router-dom";
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import ImageIcon from '@mui/icons-material/Image';
import Button from '@mui/joy/Button';


type ImageProps = {
  name: string
}

function ImageListItem({ name }: ImageProps, deleteCallback: () => void) {
  const fileDelete = () => {
    axios.delete("images/" + name)
    deleteCallback()
  }

  return (
    <ListItem>
      <ListItemAvatar>
        <Avatar>
          <ImageIcon />
        </Avatar>
      </ListItemAvatar>
      <ListItemText primary={name} />
      <Link to={"/image/" + name}>View</Link>
      <Button sx={{ mx: '5px' }} color="danger" onClick={fileDelete}>Delete</Button>
    </ListItem >
  )
}

export default function ImageList({ items, deleteCallback }: { items: ImageProps[], deleteCallback: () => void }) {
  return (
    <List sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
      {items.map((item: ImageProps) => ImageListItem(item, deleteCallback))}
    </List>
  );
}
