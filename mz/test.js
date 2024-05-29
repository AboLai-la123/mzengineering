let photos = [
    {'uri1': "asd"},
    {'uri2': "das"},
    {'uri3': "ewq"},
];

let check = "uri1";

let exists = photos.some(photo => check in photo);

console.log(exists);