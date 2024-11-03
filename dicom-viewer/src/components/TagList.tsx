import Box from '@mui/system/Box';
import Stack from '@mui/system/Stack';
import { styled } from '@mui/system';

const Item = styled('div')(({ theme }) => ({
  backgroundColor: '#D3D3D3',
  padding: theme.spacing(1),
  textAlign: 'center',
  borderRadius: 4,
  ...theme.applyStyles('dark', {
    backgroundColor: '#262B32',
  }),
}));


function TagListItem(tag: string) {
  return (
    <Item>
      {tag}
    </Item>
  )
}

export default function TagList({ tags }: { tags: string[] }) {
  return (
    <Box sx={{ width: '50%' }}>
      <Stack spacing={2}>
        {tags.map((tag: string) => TagListItem(tag))}
      </Stack>
    </Box>
  );
}
